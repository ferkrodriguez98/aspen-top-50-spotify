## ASPEN TOP 50

Las 50 canciones más escuchadas de Aspen en los últimos 7 días. Se actualiza dinámicamente usando la API de Spotify y scrapeando la web para saber que canción esta sonando.

Actualmente corre en mi computadora como una serie de cron jobs. Cada dos minutos se ejecuta el archivo main.py que scrapea la web "https://www.radios-argentinas.org/fm-aspen-1023" y con selenium obtiene el nombre de la canción que esta sonando. Luego, realizo una query con la API de Spotify que me devuelve la uri de la canción y la agrego al archivo tracks.txt. Si no consigue la uri, el nombre de la canción se agrega al archivo track_names_with_no_uri.txt. El archivo track_names.txt existe sin ninguna utilidad más que poder ver yo que canción es. 

Todos los días a las 00:00 se pushean los cambios a Git y se ejecuta el otro cron job que corre el archivo update_playlist.py. Este archivo obtiene los tracks, los shufflea en orden de cuales aparecen más, luego elimina los duplicados y devuelve los primeros 50 con los cuales actualiza la playlist. La playlist se actualiza también usando la API de Spotify. Las claves secretas para la API están en los archivos .sh que son ejecutas por el cron job, los cuales no estan subidos al repositorio. Los archivos .sh que están subidos al repositorio contienen el espacio vacío para llenar con las claves. Importante tirar un chmod 777 

Las claves para la API de Spotify se consiguen creando una app en developer.spotify.com

Desconozco totalmente si la mejor manera de realizarlo es esta, yo solo quiero ver que tan arriba está Africa de Toto.

### Got Fork?

Si estás aburrido y querés ver si la Triple T es la canción que más está sonando en la TKM podes forkear este repositorio, cambiar las credenciales, la url a la que le pegas para scrapear y listo.

### **Work in Progress**

##### Known Issues:
- El Cron no activa el virtual environment entonces tuve que instalar algunos paquetes de manera global
- Las canciones que son de publicidades a veces las agarra. Ejemplo Soda Stereo - Te hacen falta vitaminas.

##### To Do:
- Meter esto en un server y no depender de mi computadora.
- Que efectivamente sean las canciones de los últimos 7 días.
- No sé que hacer para conseguir la URI de las canciones que no devuelve nada la query porque existir existen en Spotify.