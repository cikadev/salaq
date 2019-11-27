try {
    var dropdownUser = document.querySelector('#dropdown-user');
    dropdownUser.addEventListener('click', function(event) {
      event.stopPropagation();
      dropdownUser.classList.toggle('is-active');
    });
} catch(err) {
    console.log(err);
};

var dropdownTrolley = document.querySelector('#dropdown-trolley');
dropdownTrolley.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdownTrolley.classList.toggle('is-active');
});

try {

    let media = {
        media3d: true,
        mediaImages: false,
    };

    var mediaImages = document.querySelector('#media-images');
    var media3d = document.querySelector('#media-3d');

    var viewMediaImages = document.querySelector('#view-media-images');
    var viewMedia3d = document.querySelector('#view-media-3d');

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

} catch (err) {
    console.log(err);
}

function refreshTrolley() {
    const trolleyList = document.querySelector("#trolley-list");

    trolleyList.innerHTML = "";
    fetch("/api/me/trolley")
    .then((data) => data.json())
    .then((decoded_data) => {
        decoded_data.trolley.forEach((product_trolley) => {
            trolleyList.innerHTML += `<a href="#" class="dropdown-item">${product_trolley.name} - ${product_trolley.quantity}x</a>`;
        });
    })

    refreshTrolley();
}