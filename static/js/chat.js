function send() {
  let q = document.getElementById("q").value;
  addBubble(q, "user");
  fetch("/ask", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:q})
  }).then(r=>r.json()).then(d=>{
    typeBubble(d.answer);
  });
}

function addBubble(text, cls){
  let div = document.createElement("div");
  div.className = "bubble " + cls;
  div.innerText = text;
  messages.appendChild(div);
}

function typeBubble(text){
  let div = document.createElement("div");
  div.className = "bubble ai";
  messages.appendChild(div);
  let i=0;
  let t=setInterval(()=>{
    div.innerText += text[i++];
    if(i>=text.length) clearInterval(t);
  },20);
}
