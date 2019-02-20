function btnLognForm2()
{
  app = document.getElementById('root');
  let btnLoin = document.getElementById('btnLoginForm1');
  btnLoin.style.display = 'none';
  let btnOKy = document.getElementById('btnLoginForm2');
  btnOKy.style.display = 'none';
  login = document.createElement('input');
  login.style.left = 590 + 'px';
  login.style.top = 90 + 'px';
  login.style.position = 'fixed';
  login.textContent = 'login';

  password = document.createElement('input');
  password.style.left = 590 + 'px';
  password.style.top = 150 + 'px';
  password.style.position = 'fixed';
  password.textContent = 'password';

  let h_login = document.createElement('p');
  h_login.textContent = 'My login ';
  let h_password = document.createElement('p');
  h_password.textContent = 'My password';
  h_login.style.left = 460 + 'px';
  h_login.style.top = 90 + 'px';
  h_login.style.position = 'fixed';
  h_password.style.left = 460 + 'px';
  h_password.style.top = 150 + 'px';
  h_password.style.position = 'fixed';

  app.appendChild(h_login);
  app.appendChild(login);
  app.appendChild(h_password);
  app.appendChild(password);

  let btnLogin = document.getElementById('btnLogin');
  btnLogin.style.display = 'inline-block';
  btnOK = document.getElementById('btnOK');
  btnOK.style.display = 'none';
  let btnDelete = document.getElementById('btnDelete');
  btnDelete.style.display = 'none';
  let btnSave = document.getElementById('btnSave');
  btnSave.style.display = 'none';

  let btn1 = document.getElementById('btnMovies');
  btn1.style.display = 'none';
  let btn2 = document.getElementById('btnHalls');
  btn2.style.display = 'none';
  let btn3 = document.getElementById('btnSeanses');
  btn3.style.display = 'none';
  let btn4 = document.getElementById('btnAdd');
  btn4.style.display = 'none';
}