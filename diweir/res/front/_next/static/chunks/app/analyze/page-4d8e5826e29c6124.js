(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[241,467,835,702,535,673,612],{593:function(n,o,t){Promise.resolve().then(t.bind(t,8510))},8510:function(n,o,t){"use strict";t.d(o,{default:function(){return Z}});var c=t(7437),e=t(8247),i=t(1655),a=t(4614),s=t(7398),r=t(7193),l=t(9450),p=t(983),u=t(9710),d=t(3891),m=t(393),h=t(1810);function Z(n){let{select:o}=n,t=[{action:"tasks",component:s.Z},{action:"design",component:r.Z},{action:"analyze",component:l.Z},{action:"anonymize",component:p.Z},{action:"archive",component:d.Z},{action:"purge",component:u.Z},{action:"dashboard",component:m.Z},{action:"databases",component:h.Z}];return t.forEach(n=>{n.action===o&&(n.select=!0)}),(0,c.jsx)(e.Z,{position:"static",color:"transparent",children:(0,c.jsx)("div",{children:t.map((n,o)=>(0,c.jsx)(i.Z,{title:n.action.charAt(0).toUpperCase()+n.action.slice(1),children:(0,c.jsx)(a.Z,{size:"large",onClick:()=>window.location.replace("/"+n.action),children:n.select?(0,c.jsx)(n.component,{sx:{color:"#ed6c02"}}):(0,c.jsx)(n.component,{})})},o+1))})})}}},function(n){n.O(0,[632,459,971,23,744],function(){return n(n.s=593)}),_N_E=n.O()}]);