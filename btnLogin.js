function buttonInitVisibility()
{
  let btnAdd = document.getElementById('btnAdd');
  btnAdd.style.display = 'inline-block';
  let btnOK = document.getElementById('btnOK');
  btnOK.style.display = 'none';
  let btn1 = document.getElementById('btnMovies');
  btn1.style.display = 'none';
  let btn2 = document.getElementById('btnHalls');
  btn2.style.display = 'none';
  let btn3 = document.getElementById('btnSeanses');
  btn3.style.display = 'none';
  let btn4 = document.getElementById('btnAdd');
  btn4.style.display = 'none';
}

function buttonFinalVisibility()
{
  let input = document.getElementsByTagName("input");
  let text = document.getElementsByTagName("p");
  for (i=0; i < input.length; i++)
    input[i].style.display = 'none';
  for (i=0; i < text.length; i++)
    text[i].style.display = 'none';
  let btn = document.getElementById('btnLogin');
  btn.style.display = 'none';
}

function btnLogn()
{
  let app = document.getElementById('root');
  let login = '';
  let password = '';

  for (i=0; i < app.childElementCount; i++)
  {
    let cur = app.childNodes[i];
    if (cur.textContent == 'login')
      login = cur.value;
    if (cur.textContent == 'password')
      password = cur.value;
  }

  var request = new XMLHttpRequest();
  request.open('POST', 'http://localhost:5004/api/1.0/login', true);
  request.setRequestHeader("Content-Type", "application/json");
  request.onload = function () {

    var data = JSON.parse(this.response);
    token = data['Result'];
    console.log("token", token);
    if (token == null)
    {
      alert("Wrong login or password!");
      return true;
    }
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    info = JSON.parse(window.atob(base64));
    console.log(info);
    console.log("exp ", info.exp);
    var current_time = new Date().getTime() / 1000;
    console.log("time ", current_time);
    if (current_time < info.exp)
      console.log("OK");
    else
      console.log("Not OK");

    buttonFinalVisibility();
    btnMovies();
  }
  data = JSON.stringify({'login': login, 'password': password});
  resp = request.send(data);

  return true;

}