from typing import Any
from django.utils.timezone import now
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from utils.utils import generate_course_identifier_name

from django.core.validators import MaxValueValidator, MinValueValidator

from functools import reduce

from profiles.models import Alumno, Profesor


class Dia(models.Model):
    WEEKDAYS = [
        ("LUN", "Lunes"),
        ("MAR", "Martes"),
        ("MIE", "Miércoles"),
        ("JUE", "Jueves"),
        ("VIE", "Viernes"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]
    name = models.CharField(max_length=3, choices=WEEKDAYS)
    id=models.IntegerField(primary_key=True)
    def __str__(self) -> str:
        return self.name


class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="cursos", null=True, blank=True)
    activo = models.BooleanField(default=True)
    payout_ratio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MaxValueValidator(1, "El valor debe estar entre 1 y 0."),
            MinValueValidator(0, "El valor debe estar entre 1 y 0."),
        ],
        default=0.5,
    )
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("detail-course", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def amount_receivable(self):
        groups = self.grupo_set.all()
        receivable = 0
        for group in groups:
            receivable += group.amount_receivable
        return receivable



class Previa(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="curso")
    previa = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="previa")


class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    duracion_meses = models.IntegerField()
    fecha_baja = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to="carreras", null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    activo = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("careers")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class AlumnoCurso(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_finalizado = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)
    fee = models.DecimalField(max_digits=7 ,decimal_places=2, default=1, validators=[
        MinValueValidator(0, "La cuota real debe ser mayor a 0."),
        MaxValueValidator(50000, "La cuota real debe ser menor a $50000.")])

    def __str__(self):
        return f"Inscripcion: {self.alumno.apellido} -> {self.curso.nombre}"

    class Meta:
        ordering = ["-fecha_inscripcion"]


class AlumnoCarrera(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_finalizado = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return "Inscripcion: " + self.alumno.nombre + " " + self.curso.nombre


class Salon(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"nombre": "Ya existe un registro con este nombre."},
    )
    capacidad = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1, "La capacidad debe ser mayor o igual a 1."),
            MaxValueValidator(500, "La capacidad debe ser menor o igual a 500."),
        ],
    )
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    id=models.AutoField(primary_key=True)
    identificador=models.CharField(max_length=30, blank=True, null=True)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno, blank=True) #validar que el alumno este inscripto en el curso, y que la cantidad sea menor o igual al cupo de la clase
    cupo=models.IntegerField(null=False,default=1,validators=[MinValueValidator(1, "La cantidad de alumnos debe estar entre 1 y 50"),MaxValueValidator(50,"La cantidad de alumnos debe estar entre 1 y 50")])
    profesores=models.ManyToManyField(Profesor) #validar que el profesor este asignado al curso
    fecha_inicio = models.DateTimeField(null=False, blank=False, default=now)
    fecha_baja=models.DateTimeField(null=True, blank=True)
    activo=models.BooleanField(default=True)

    def is_inactive(self):
        return self.fecha_baja and self.fecha_baja <= now()

    def save(self, *args, **kwargs):
        if not self.activo:
            # If "Activo" checkbox is unchecked, set fecha_baja to the current date
            self.fecha_baja = now()
        elif self.is_inactive():
            # If fecha_baja has passed, set activo to False
            self.activo = False
        super().save(*args, **kwargs)


    def __str__(self) -> str:

            return f"Identificador: {self.identificador} - Curso: {self.curso.nombre} - Activo: {self.activo}"


    def get_absolute_url(self):
        return reverse("clases:detail-group", kwargs={"pk": self.pk})

    @property
    def generate_identificador(self):
        print(f"Generando identificador para GRUPO {self.id}")
        group_identifier=generate_course_identifier_name(self.curso.nombre)
        print(f"Identificador generado {group_identifier}")
        bloques_de_clase = BloqueDeClase.objects.filter(grupo=self)
        print(f"bloques_de_clase {bloques_de_clase}")
        if bloques_de_clase:
            for bloque in bloques_de_clase:
                day_names = [dia.name.lower() for dia in bloque.dia.all()]
                if len(day_names) >=1:
                    days_initials=[]
                    for day_name in day_names:
                        if "mie" in day_name:
                            day_initial = "X"
                        else:
                            # Use the first letter of the other day names
                            day_initial = day_name[0][0].upper()
                        days_initials.append(day_initial)
                    group_identifier += "".join(days_initials)
                    group_identifier += f"{bloque.hora_inicio.strftime('%H%M')}S{bloque.salon.nombre}"
        print(f"Identificador final {group_identifier}")
        self.identificador=group_identifier
        print(f"Identificador actualizado {self.identificador}")
        self.save()

    @property
    def amount_payable(self):
        if self.alumnos.count() > 0:
            return self.curso.costo * self.curso.payout_ratio * self.alumnos.count()
        else:
            return 0
    @property
    def amount_receivable(self):
        receivable = 0
        for student in self.alumnos.all():
            enrolment = student.alumnocurso_set.get (curso=self.curso)
            if enrolment.fecha_finalizado == None:
                receivable += enrolment.fee
        return receivable


class BloqueDeClase(models.Model):
    id=models.AutoField(primary_key=True)
    dia = models.ManyToManyField(Dia)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        # Set or update the group identifier
        super().save(*args, **kwargs)
        # self.grupo.generate_identificador()

    def delete(self, using=None, keep_parents=False):


        return super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"Bloque id: {self.id} - Dias: {', '.join([dia.name for dia in self.dia.all()])} - Hora inicio: {self.hora_inicio} - Hora fin: {self.hora_fin} - Grupo: {self.grupo} - Salon: {self.salon}"

class Leccion(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    alumnos = models.ManyToManyField(Alumno, blank=True)
    profesores = models.ManyToManyField(Profesor, blank=True)
    bloque = models.ForeignKey(BloqueDeClase, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    descripcion = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return (
            f"Lección: {self.grupo} {self.bloque.hora_inicio} - {self.bloque.hora_fin}"
        )

    class Meta:
        verbose_name_plural = "Lecciones"


class Examen(models.Model):
    fecha_examen = models.DateTimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Examen: {self.curso.nombre} - {self.fecha_examen}"

    class Meta:
        verbose_name_plural = "Exámenes"


class AlumnoExamen(models.Model):
    inscripcion = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    fallo = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(10, "La nota máxima permitida es 10."),
            MinValueValidator(1, "La nota mínima permitida es 1."),
        ],
        null=True,
        blank=True,
    )
    comentario = models.TextField(max_length=250, blank=True, null=True)

    @property
    def aprobado(self):
        return self.fallo > 4

    def __str__(self) -> str:
        return f"Fallo de examen {self.examen.curso.nombre} {self.examen.fecha_examen}: {self.inscripcion.alumno.apellido}, {self.inscripcion.alumno.nombre}. {self.fallo}."

    class Meta:
        verbose_name_plural = "Fallos"


class Pago(models.Model):
    id=models.AutoField(primary_key=True)
    alumno=models.ForeignKey(Alumno, on_delete=models.CASCADE)
    monto=models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(1, "El monto debe ser mayor que cero"),MaxValueValidator(1000000,"El monto no debe superar el millón de pesos")])
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    fecha=models.DateTimeField(null=False, blank=False, default=now)
    descripcion=models.TextField(max_length=250, blank=True, null=True)
    comprobante=models.FileField(upload_to='pagos', null=True, blank=True)

    def __str__(self):
        return f"Pago:{self.id} {self.alumno} {self.monto} {self.fecha}"

    class Meta:
        ordering = ["-fecha"]


class FaltaProfesor(models.Model):
    profesor_titular=models.ForeignKey(Profesor, on_delete=models.CASCADE)
    profesor_suplente=models.ForeignKey(Profesor, on_delete=models.CASCADE,blank=True, null=True, related_name="substituto")
    grupo=models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    descripcion=models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"Falta: {self.profesor_titular} {self.fecha}"

    class Meta:
        ordering = ["-fecha"]