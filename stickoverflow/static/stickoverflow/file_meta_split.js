function getCmaFileInfo(obj,stype) {
   var fileObj, pathHeader , pathMiddle, pathEnd, allFilename, fileName, extName;
   if(obj == "[object HTMLInputElement]") {
       fileObj = obj.value
   } else {
       fileObj = document.getElementById(obj).value;
   }
   if (fileObj != "") {
           pathHeader = fileObj.lastIndexOf("\\");
           pathMiddle = fileObj.lastIndexOf(".");
           pathEnd = fileObj.length;
           fileName = fileObj.substring(pathHeader+1, pathMiddle);
           extName = fileObj.substring(pathMiddle+1, pathEnd);
           allFilename = fileName+"."+extName;

           if(stype == "all") {
                   return allFilename; // 확장자 포함 파일명
           } else if(stype == "name") {
                   return fileName; // 순수 파일명만(확장자 제외)
           } else if(stype == "ext") {
                   return extName; // 확장자
           } else {
                   return fileName; // 순수 파일명만(확장자 제외)
           }
   } else {
           alert("파일을 선택해주세요");
           return false;
   }
   // getCmaFileView(this,'name');
   // getCmaFileView('upFile','all');
}

function getCmaFileView(obj,stype) {
   var s = getCmaFileInfo(obj,stype);
   alert(s);
}
