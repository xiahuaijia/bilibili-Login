function load_publicKey(){
$.getJSON("/bilibili_Login/ajax.php?act=getkey&ts=" + new Date().getTime(), function (rs) {
	if (rs && rs.error) {
		console.info("服务端出现异常，请稍后重试");
	} else {
		  var jscrypt = new JSEncrypt();
		  jscrypt.setPublicKey(rs.key);
		  Basepasswd = getQueryString("passwd");
		  sign = checksign(getQueryString("sign"),Basepasswd);
		  if (Basepasswd && sign) {
		  	passwd = utf8to16(base64decode(Basepasswd));
		  	/*console.info(passwd);*/
		  	passwd = jscrypt.encrypt(rs.hash + passwd);
		  	/*console.info(passwd);*/
		  	document.write(passwd);
		  }else{
		  	document.write("参数错误");
		  }
		}
	})
}
function getQueryString(name) { 
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
	var r = window.location.search.substr(1).match(reg); 
	if (r != null) return unescape(r[2]); return null; 
}
