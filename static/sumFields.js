function sumFields() {
  let request = new XMLHttpRequest();
  let symbol = document.getElementById("buy_symbol").value
  request.open("GET", `https://api.iextrading.com/1.0/stock/${symbol}/quote`)
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
      let shares = parseInt(document.getElementById("shares").value)
      let total = formatter.format(priceParsed * shares)
      let NaNMessage = "Invalid symbol"
      if (Number.isNaN(priceParsed)){
        return document.getElementById("total").innerHTML = `${NaNMessage}`
      }
      else {
        return document.getElementById("total").innerHTML = `Purchase ${shares} shares of ${companyName} common stock for ${total}?`
      }

    }
  }
}














