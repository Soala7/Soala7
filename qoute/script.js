async function getQuote() {
  const category = document.getElementById("category").value;

  //console.log(category);
  const quoteText = document.getElementById("quote");
  const quoteAuthor = document.getElementById("author");

  quoteText.textContent = "Loading...";
  quoteAuthor.textContent = "";

  try {
    const res = await fetch('https://api.quotable.io/quotes/random');
    const data = await res.json();

    //console.log(data);

    quoteText.innerHTML = '"' + data[0].content + '"';
    quoteAuthor.innerHTML = "– " + data[0].author;
  } catch (err) {
    quoteText.textContent = "Could not fetch quote. Please try again.";
    quoteAuthor.textContent = "";
    console.error(err);
  }
}
