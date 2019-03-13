function sumFields() {
  let symbol = document.getElementById("buy_symbol").value
  let shares = parseInt(document.getElementById("shares").value)
  let data = `https://api.iextrading.com/1.0/stock/${symbol}/quote`
  let total = shares * parseInt(data["LatestSalePrice"])

  if (data != null) {
    document.getElementById("total").innerHTML(total)
  }
  else {
    ocument.getElementById("total").innerHTML("Invalid Symbol")
  }


}










