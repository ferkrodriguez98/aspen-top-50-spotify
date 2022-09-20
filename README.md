## RADIOS ARGENTINAS TOP 50

Las 50 canciones más escuchadas en Aspen, Vorterix, Rock & Pop, Radio Blue y Mega en los últimos 7 días. Las playlists se actualizan dinámicamente cada 6 horas usando la API de Spotify y scrapeando la web para saber que canción esta sonando.

- Aspen: https://open.spotify.com/playlist/7bZVSBqJalnab6Yl6bGk3a?si=4a2d479a1c1a4255
- Vorterix: https://open.spotify.com/playlist/5yWsFE5mNDxV0ljNWX2EdR?si=334030a2d77f443b
- Rock & Pop: https://open.spotify.com/playlist/3n1KqCxQ7J1WxDegFgTbJy?si=551eaf958e174fb4
- Radio Blue: https://open.spotify.com/playlist/4L1aOpoWD9MKwcYT3vckdZ?si=46162d44119e4901
- Mega: https://open.spotify.com/playlist/1zOvjRzzkfz2YAkJII1keY?si=87d8d3b73c054ba8

Actualmente corre en mi computadora como una serie de cron jobs. Cada dos minutos se ejecuta el archivo main.py que scrapea la web "https://www.radios-argentinas.org/fm-aspen-1023" (en el caso de aspen) y con selenium obtiene el nombre de la canción que esta sonando. Luego, realizo una query con la API de Spotify que me devuelve la uri de la canción y la agrego al archivo tracks.txt. Si no consigue la uri, el nombre de la canción se agrega al archivo track_names_with_no_uri.txt. El archivo track_names.txt existe sin ninguna utilidad más que poder ver yo que canción es. 

Cada 6 horas se ejecuta el otro cron job que corre el archivo update_playlist.py. Este archivo obtiene los tracks, los shufflea en orden de cuales aparecen más, luego elimina los duplicados y devuelve los primeros 50 con los cuales actualiza la playlist. La playlist se actualiza también usando la API de Spotify. Las claves secretas para la API están en los archivos .sh que son ejecutas por el cron job, los cuales no estan subidos al repositorio. Los archivos .sh que están subidos al repositorio contienen el espacio vacío para llenar con las claves. Todos los días a las 00:00 se pushean los cambios a Git.

### Importante!

- No olvidar tirar un chmod 777 en los archivos .sh
- Si queres pushear automáticamente desde un cron, tenes que agregar la clave ssh y tirar en la terminal un "ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts" para que no te rebote.
- Las claves para la API de Spotify se consiguen creando una app en developer.spotify.com
- Desconozco totalmente si la mejor manera de realizarlo es esta, yo solo quiero ver que tan arriba está Africa de Toto en Aspen.

### Got Fork?

Si estás aburrido y querés ver si la Triple T es la canción que más está sonando en la TKM podes forkear este repositorio, cambiar las credenciales, agregar una linea abajo de todo en main.py y listo.

### **Work in Progress**

##### Known Issues:
- El Cron no activa el virtual environment entonces tuve que instalar algunos paquetes de manera global
- Las canciones que son de publicidades a veces las agarra. Ejemplo Soda Stereo - Te hacen falta vitaminas para no se que pastilla o Paisaje de Gilda que no se de que publicidad es. Actualmente lo soluciono directamente obviandolas pero está técnicamente mal.
- Las canciones que son de cortinas musicales también son otro problema. Hay varios temas del capo de Terry Devine King (el que hizo el soundtrack de Iron Man) que algun programa de Vorterix usa de cortina.
- Hay canciones que le pega a la api de spotify y devuelve una uri de otra versión falopa y no de la original. Ejemplo can't buy me love de los beatles o clocks de coldplay que devuelve de un album compilado raro.

##### To Do:
- Meter esto en un server y no depender de mi computadora.
- Que efectivamente sean las canciones de los últimos 7 días y no un estimado.
- No sé que hacer para conseguir la URI de las canciones que no devuelve nada la query porque existir existen en Spotify. La mejor manera de hacerlo por ahora fue mandar en la query directamente track + artist y sacar los () donde a veces decia Remastered 2009 o alguna cosa del estilo, esto bajo muchísimo la cantidad de canciones que no devolvían uri.
- Ampliar a mas radios?