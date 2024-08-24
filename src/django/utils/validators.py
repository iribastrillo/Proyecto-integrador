import ipaddress
import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import punycode
from django.utils.ipv6 import is_valid_ipv6_address
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _


EMPTY_VALUES = (None, "", [], (), {})

@deconstructible
class EmailValidator:
    message = _("Enter a valid email address.")
    code = "invalid"
    user_regex = _lazy_re_compile(
        # dot-atom
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])'
        r'*"\Z)',
        re.IGNORECASE,
    )
    domain_regex = _lazy_re_compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
        re.IGNORECASE,
    )
    literal_regex = _lazy_re_compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r"\[([A-F0-9:.]+)\]\Z",
        re.IGNORECASE,
    )
    domain_allowlist = ["localhost"]

    def __init__(self, message=None, code=None, allowlist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowlist is not None:
            self.domain_allowlist = allowlist

    def __call__(self, value):
        # The maximum length of an email is 320 characters per RFC 3696
        # section 3.
        if not value or "@" not in value or len(value) > 320:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(
            domain_part
        ):
            # Try for possible IDN domain-part
            try:
                domain_part = punycode(domain_part)
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match[1]
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass
        return False

    def __eq__(self, other):
        return (
            isinstance(other, EmailValidator)
            and (set(self.domain_allowlist) == set(other.domain_allowlist))
            and (self.message == other.message)
            and (self.code == other.code)
        )


def validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise ValidationError(
            _("Enter a valid %(protocol)s address."),
            code="invalid",
            params={"protocol": _("IPv4"), "value": value},
        )


def validate_ipv6_address(value):
    if not is_valid_ipv6_address(value):
        raise ValidationError(
            _("Enter a valid %(protocol)s address."),
            code="invalid",
            params={"protocol": _("IPv6"), "value": value},
        )


def validate_ipv46_address(value):
    try:
        validate_ipv4_address(value)
    except ValidationError:
        try:
            validate_ipv6_address(value)
        except ValidationError:
            raise ValidationError(
                _("Enter a valid %(protocol)s address."),
                code="invalid",
                params={"protocol": _("IPv4 or IPv6"), "value": value},
            )


ip_address_validator_map = {
    "both": [validate_ipv46_address],
    "ipv4": [validate_ipv4_address],
    "ipv6": [validate_ipv6_address],
}


def ip_address_validators(protocol, unpack_ipv4):
    """
    Depending on the given parameters, return the appropriate validators for
    the GenericIPAddressField.
    """
    if protocol != "both" and unpack_ipv4:
        raise ValueError(
            "You can only use `unpack_ipv4` if `protocol` is set to 'both'"
        )
    try:
        return ip_address_validator_map[protocol.lower()]
    except KeyError:
        raise ValueError(
            "The protocol '%s' is unknown. Supported: %s"
            % (protocol, list(ip_address_validator_map))
        )
