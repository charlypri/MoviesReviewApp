// /*
//	* Licensed to the Apache Software Foundation (ASF) under one
//	* or more contributor license agreements.	See the NOTICE file
//	* distributed with this work for additional information
//	* regarding copyright ownership.	The ASF licenses this file
//	* to you under the Apache License, Version 2.0 (the
//	* "License"); you may not use this file except in compliance
//	* with the License.	You may obtain a copy of the License at
//	*
//	* http://www.apache.org/licenses/LICENSE-2.0
//	*
//	* Unless required by applicable law or agreed to in writing,
//	* software distributed under the License is distributed on an
//	* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
//	* KIND, either express or implied.	See the License for the
//	* specific language governing permissions and limitations
//	* under the License.
//	*/
// var app = {
//		 // Application Constructor
//		 initialize: function() {
//				 document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
//		 },

//		 // deviceready Event Handler
//		 //
//		 // Bind any cordova events here. Common events are:
//		 // 'pause', 'resume', etc.
//		 onDeviceReady: function() {
//				 this.receivedEvent('deviceready');
//		 },

//		 // Update DOM on a Received Event
//		 receivedEvent: function(id) {
//				 var parentElement = document.getElementById(id);
//				 var listeningElement = parentElement.querySelector('.listening');
//				 var receivedElement = parentElement.querySelector('.received');

//				 listeningElement.setAttribute('style', 'display:none;');
//				 receivedElement.setAttribute('style', 'display:block;');

//				 console.log('Received Event: ' + id);
//		 }
// };

// app.initialize();
//



async function inicio() {
  let main = document.querySelector(".inicio");
  let peli = document.querySelector(".mainPeli");
  window.scrollTo(0,0);
  main.style.display = "block";
  peli.style.display = "none";
  document.querySelector('#puntacionTotal').innerText = "esperando puntuacion";
  document.querySelector("#mostrarSpoilersB").style.display = "none";

  try{
  document.querySelector(".resultadosPelis").innerHTML = "";

  let div0=document.querySelector("#opinionesTabla").firstElementChild;
  document.querySelector("#opinionesTabla").innerHTML = "";
  document.querySelector("#opinionesTabla").appendChild(div0);

  document.querySelector("#twitter").style.visibility="hidden";
  document.querySelector("#opiniones").style.visibility="hidden";

  let div1=document.querySelector("#opP").firstElementChild;
  let div2=document.querySelector("#opN").firstElementChild;
  let div3=document.querySelector("#opM").firstElementChild;

  document.querySelector("#opP").innerHTML="";
  document.querySelector("#opN").innerHTML="";
  document.querySelector("#opM").innerHTML="";

  document.querySelector("#opP").appendChild(div1);
  document.querySelector("#opN").appendChild(div2);
  document.querySelector("#opM").appendChild(div3);

  document.querySelector("#porcP").innerText = "";
  document.querySelector("#porcN").innerText = "";
  document.querySelector("#porcM").innerText = "";
}catch(e){
  console.log(e);
}
  


  document.querySelector('#puntacionTotal').style.color = "grey";

  let pelis = await todasPelis();

  console.log(pelis);
  pelis.forEach(element => {
    let p1 = crearResultadoPeli(element.name, element.id);
    let div = document.querySelector(".resultadosPelis");
    //console.log(div);
    div.appendChild(p1);
  });

}

function mostrarPeli() {
  
  let main = document.querySelector(".inicio");
  let peli = document.querySelector(".mainPeli");
  main.style.display = "none";
  peli.style.display = "flex";

}



document.querySelector(".zonaSpoilers").style.visibility = "hidden";

/*Funcion para mostar y ocultar spoilers */
function mostrarSpoilers(event) {
  let zonaSpoilers = document.querySelector(".zonaSpoilers");

  if (zonaSpoilers.style.visibility == "hidden") {
    document.querySelector("#twitter").style.visibility="visible";
    document.querySelector("#opiniones").style.visibility="visible";
    zonaSpoilers.style.visibility = "visible";
  } else {
    zonaSpoilers.style.visibility = "hidden";
    document.querySelector("#twitter").style.visibility="hidden";
    document.querySelector("#opiniones").style.visibility="hidden";
  }
}


async function masInfo(event) {
  let titulo = event.target.innerHTML;
  console.log(titulo);
  let id = event.target.parentElement.id;
  console.log(id);



  mostrarPeli();
  document.querySelector('#tituloPeli').innerText = titulo;
  document.querySelector("#mostrarSpoilersB").style.display = "block";

  setTimeout(function(){ window.scrollTo(0,0); }, 100);

  let punt = "";
  let name = "";
  await puntuaciones(id).then(resp => {
    console.log(resp);
    if (resp.status == 404) {
      punt = "puntuacion no disponible";
    }
    else {
      punt = resp.Puntuacion;
      name = resp.name;
    }
  }).catch(function (error) {
    console.log('Hubo un problema ' + error.message)
  });
  console.log(punt);
  document.querySelector('#puntacionTotal').innerText = punt;
  switch (true) {
    case (punt < 5):
      document.querySelector('#puntacionTotal').style.color = "red";
      break;
    case (punt >= 5 && punt < 7):
      document.querySelector('#puntacionTotal').style.color = "yellow";
      break;
    case (punt >= 7 && punt < 9):
      document.querySelector('#puntacionTotal').style.color = "green";
      break;
    case (punt >= 9):
      document.querySelector('#puntacionTotal').style.color = "blue";
      break;
    default:
      document.querySelector('#puntacionTotal').style.color = "grey";
      break;
  }
  let opinionesR = [];

  await opiniones(id).then(resp => {
    console.log(resp);
    if (resp.status == 404) {
      opinionesR = "no hay opiniones";
    }
    else {
      opinionesR = resp.Criticas;
    }
  }).catch(function (error) {
    console.log('Hubo un problema ' + error.message)
  });
  let divOpiniones = document.querySelector("#opinionesTabla");
  let div0=document.querySelector("#opinionesTabla").firstElementChild;
  document.querySelector("#opinionesTabla").innerHTML = "";
  document.querySelector("#opinionesTabla").appendChild(div0);
  opinionesR.forEach(element => {
    if (!element.includes('&')) {
      let fila = document.createElement("tr");
      let celda = document.createElement("td");
      celda.innerText = element;
      fila.appendChild(celda);
      divOpiniones.appendChild(fila);
    }

  });


  let porcentajeP = "n/a", porcentajeN = "n/a", porcentajeM = "n/a";
  let tweetsP = [], tweetsN = [], tweetsM = [];
  await twitter(id).then(resp => {
    console.log(resp[name][0]);
    if (resp.status == 404) {
      porcentajeM = "n/a";
      porcentajeP = "n/a";
      porcentajeN = "n/a";
      tweetsP = [];
      tweetsM = [];
      tweetsN = [];
    }
    else {
      porcentajeM = resp[name][0].PorcentajeTweetsNegativos;
      porcentajeP = resp[name][0].PorcentajeTweetsPositivos;
      porcentajeN = resp[name][0].PorcentajeTweetsNeutros;
      tweetsP = resp[name][0].TweetsBuenos;
      tweetsM = resp[name][0].TweetsMaloss;
      tweetsN = resp[name][0].TweetsNeutros;
    }
  }).catch(function (error) {
    console.log('Hubo un problema ' + error.message)
  });

  document.querySelector("#porcP").innerText = porcentajeP;
  document.querySelector("#porcN").innerText = porcentajeN;
  document.querySelector("#porcM").innerText = porcentajeM;

  let divTwitter;
  divTwitter = document.querySelector("#opP");
  tweetsP.forEach(element => {
    if (!element.includes('&')) {
      let fila = document.createElement("tr");
      let celda = document.createElement("td");
      celda.innerText = element;
      fila.appendChild(celda);
      divTwitter.appendChild(fila);
    }
  });

  divTwitter = document.querySelector("#opN");
  tweetsN.forEach(element => {
    if (!element.includes('&')) {
      let fila = document.createElement("tr");
      let celda = document.createElement("td");
      celda.innerText = element;
      fila.appendChild(celda);
      divTwitter.appendChild(fila);
    }
  });

  divTwitter = document.querySelector("#opM");
  tweetsM.forEach(element => {
    if (!element.includes('&')) {
      let fila = document.createElement("tr");
      let celda = document.createElement("td");
      celda.innerText = element;
      fila.appendChild(celda);
      divTwitter.appendChild(fila);
    }
  });




  document.querySelector("#mostrarSpoilersB").style.display = "block";
  




}

//Crea un resultado de peli, dado un título
function crearResultadoPeli(titulo, id) {
  let div1 = document.createElement("div");
  div1.className = "resultadoPeli";
  div1.setAttribute('id', id);
  let tit = document.createElement("span");
  tit.innerText = titulo;
  div1.appendChild(tit);
  let img2 = document.createElement("img");
  img2.setAttribute("src", "/img/info.svg");
  tit.addEventListener("click", masInfo);
  img2.className = "masInfo";
  div1.appendChild(img2);

  return div1;
}

async function puntuaciones(id) {
  let resp = await fetch('http://localhost:5002/movies/' + id + '/rating', { method: 'GET' })
    .catch(function (error) {
      console.log('Hubo un problema con la petición Fetch:' + error.message)
    });
  let respuesta = resp.json();
  return respuesta;
}


async function todasPelis() {
  let resp = await fetch('http://localhost:5002/movies', { method: 'GET' })
    .catch(function (error) {
      console.log('Hubo un problema con la petición Fetch:' + error.message)
    });
  let respuesta = resp.json();
  return respuesta;
}

async function opiniones(id) {
  let resp = await fetch('http://localhost:5002/movies/' + id + '/opinions', { method: 'GET' })
    .catch(function (error) {
      console.log('Hubo un problema con la petición Fetch:' + error.message)
    });
  let respuesta = resp.json();
  return respuesta;
}

async function twitter(id) {
  let resp = await fetch('http://localhost:5002/movies/' + id + '/twitter', { method: 'GET' })
    .catch(function (error) {
      console.log('Hubo un problema con la petición Fetch:' + error.message)
    });
  let respuesta = resp.json();
  return respuesta;
}




async function mostrarPelis(peli) {
  document.querySelector(".resultadosPelis").innerHTML = "";
  let pelis = await todasPelis();

  console.log(pelis);
  pelis.forEach(element => {
    if (element.name.toLowerCase().includes(peli.toLowerCase())) {

      let p1 = crearResultadoPeli(element.name, element.id);
      let div = document.querySelector(".resultadosPelis");
      //console.log(div);
      div.appendChild(p1);

    }

  });

}

/*Funcion para capturar la busqueda del elemento de la caja */
function buscar(event) {
  event.preventDefault();
  let texto = document.getElementById("campoBuscar").value;
  document.getElementById("campoBuscar").value = "";
  mostrarPelis(texto);
  setTimeout(function(){ window.scrollTo(0,window.innerHeight-200); }, 100);
  
}




/*Funcion main*/

document.addEventListener("deviceready", async function () {
  //Aqui va el codigo de JS


  let iniciando = await inicio();

});






document.querySelector("#botonBuscar").addEventListener("click", buscar);
document.querySelector("#big-button").addEventListener("click", inicio);
document
  .querySelector("#mostrarSpoilersB")
  .addEventListener("click", mostrarSpoilers);
//document.querySelector("#tituloWeb").addEventListener("click", inicio);
//document.querySelector("#campoBuscar").addEventListener("keypress",mostrarPelis);
