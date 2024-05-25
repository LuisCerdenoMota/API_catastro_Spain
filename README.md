## Descripción
Este script llamará a la API de Catastro español (no país vasco ni navarra).

Se usa como input un excel que hay en la misma ruta llamado input.xlsx. Este excel debe tener una columna llamada ReferenciaCatastral para obtener una lista de referencias catastrales. Dentro de esa lista se puede incluir tanto matrices como referencias catastrales únicas.

El producto final es un excel datado que se genera en la carpeta output con el resultado de la ejecución.
En este excel solo se mostrarán los resultados de las referencias para las que se ha podido obtener un resultado, es decir, no tendremos las referencias para las que no se ha podido llamar o se haya producido algún error. 

El funcionamiento de la API del catastro nacional viene descrito en su documentación, ver la carpeta "Documentación API".

## Mejoras futuras:
* Incluir en el excel del output las referencias catastrales que fallaron y no solo las referencias para las que se pudo llamar correctamente.
* Renombre de columnas para mejor comprensión del output