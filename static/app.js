"use strict";

// format '{ "name" : "root", "children" : [ "C1", {"name" : "bb", "children": ["aa"]} ] }'

function createName(content){
  var n = document.createElement("div");
  n.className = "name";
  n.appendChild(document.createTextNode(content));
  return n;
}


function clear(node){
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}


function renderTree(t, e){
  clear(t);
  var n = document.createElement("div");

  var name = t.name;
  var children = t.children;

  if ( children ){
    n.className = "elem";
    n.appendChild(createName(name));
    n.text = name;
    children.forEach(function(c){
      var cn = document.createElement("div");
      cn.className = "child";
      renderTree(c, cn);
      n.appendChild(cn);
    });
  } else {
    n.className = "leaf";
    n.appendChild(createName(t));
  }

  e.appendChild(n);
}
