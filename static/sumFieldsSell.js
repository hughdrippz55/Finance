function sumFieldsSell() {
  let request = new XMLHttpRequest();
  let symbol = document.getElementById("stocks").value.split(", ")
  request.open("GET", `https://api.iextrading.com/1.0/stock/${symbol[0]}/quote`)
  request.send(null);
  request.onreadystatechange = callbackFunction;

  function callbackFunction(){
    if (request.readyState == 4 && request.status != 404){
      var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      let data = JSON.parse(request.responseText)
      let priceParsed = parseFloat(data["latestPrice"])
      let companyName = data["companyName"]
      let shares = parseInt(document.getElementById("sharesSell").value)
      let total = formatter.format(priceParsed * shares)
      let NaNMessage = "Invalid symbol"
        return document.getElementById("total").innerHTML = `Purchase ${shares} shares of ${companyName} common stock for ${total}?`
      }

    }
  }















