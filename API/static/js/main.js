const form = document.getElementById("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const artist = document.getElementById("artist").value;
  const popularity = document.getElementById("popularity").value;
  const random = document.getElementById("random").checked;
  const apiUrl = `https://verserator.deta.dev/api/v1/${artist}?lyric=random&popularity=${popularity}`;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });
});

