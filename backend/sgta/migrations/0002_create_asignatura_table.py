# Generated manually to create missing asignatura table

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgta', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS `sgta_asignatura` (
                `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                `codigo` varchar(10) NOT NULL UNIQUE,
                `nombre` varchar(200) NOT NULL,
                `descripcion` longtext,
                `activa` bool NOT NULL,
                `registrada_por_id` bigint,
                `fecha_creacion` datetime(6) NOT NULL,
                CONSTRAINT `sgta_asignatura_registrada_por_id_fk` 
                    FOREIGN KEY (`registrada_por_id`) 
                    REFERENCES `sgta_usuario` (`id`)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS `sgta_asignatura`;"
        ),
    ]
