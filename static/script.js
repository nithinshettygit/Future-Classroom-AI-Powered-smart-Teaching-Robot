async function askQuestion() {
  const query = document.getElementById("query").value;
  if (!query) {
      alert("Please enter a question.");
      return;
  }
  
  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "Loading...";
  responseDiv.classList.remove("hidden");
  
  try {
      const response = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query })
      });

      const data = await response.json();
      responseDiv.innerHTML = data.response || "Error: " + data.error;
  } catch (error) {
      responseDiv.innerHTML = "Failed to fetch response.";
  }
}
