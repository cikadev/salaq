let media = {
    media3d: true,
    mediaImages: false,
};

var mediaImages = document.querySelector('#media-images');
var media3d = document.querySelector('#media-3d');

var viewMediaImages = document.querySelector('#view-media-images');
var viewMedia3d = document.querySelector('#view-media-3d');

if (mediaImages !== undefined) {
    mediaImages.addEventListener('click', function(event) {
      event.stopPropagation();
      if (!media.mediaImages)
      {
        media3d.classList.remove('is-active');
        mediaImages.classList.add('is-active');

        viewMediaImages.classList.remove('is-invisible');
        viewMedia3d.classList.add('is-invisible');

        media.media3d = false;
        media.mediaImages = true;
      }
    });
}

if (media3d != undefined) {
    media3d.addEventListener('click', function(event) {
      event.stopPropagation();
      if (!media.media3d)
      {
        media3d.classList.add('is-active');
        mediaImages.classList.remove('is-active');

        viewMediaImages.classList.add('is-invisible');
        viewMedia3d.classList.remove('is-invisible');

        media.media3d = true;
        media.mediaImages = false;
      }
    });
}