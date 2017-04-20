using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;

namespace Dal.bi {
    /// <summary>
    /// 登录B站
    /// RSA加密算法来自于http://blog.csdn.net/u010678947/article/details/48652875，感谢
    /// 
    /// 登录步骤：
    /// 1、调用getVerCodeImage，获取验证码图片；
    /// 2、调用LoginBilibili进行登录
    /// </summary>
    public static class Login {
        static CookieContainer Cookie = new CookieContainer();
        static void Init() {
            HttpWebRequest WebQ = (HttpWebRequest)WebRequest.Create("http://passport.bilibili.com/ajax/miniLogin/minilogin?t=" + new Random().NextDouble().ToString());
            Cookie = new CookieContainer();
            WebQ.CookieContainer = Cookie;
            using (var WebR = (HttpWebResponse)WebQ.GetResponse()) {
                StreamReader reader = new StreamReader(WebR.GetResponseStream(), Encoding.Default);
                string HTML = reader.ReadToEnd();
                Cookie = WebQ.CookieContainer;
            }
        }

        /// <summary>
        /// 获取RSA公钥
        /// </summary>
        /// <returns></returns>
        static string GetPublicKey(out string hash) {
            HttpWebRequest WebQ = (HttpWebRequest)WebRequest.Create("http://passport.bilibili.com/login?act=getkey&_=" + new Random().NextDouble().ToString());
            WebQ.CookieContainer = Cookie;
            using (var WebR = (HttpWebResponse)WebQ.GetResponse()) {
                StreamReader reader = new StreamReader(WebR.GetResponseStream(), Encoding.Default);
                string HTML = reader.ReadToEnd();
                string Key = Common.NewC.GetString(HTML, "\"key\":\"", "\"}", false, 0);
                hash = Common.NewC.GetString(HTML, "\"hash\":\"", "\",", false, 0);
                Cookie = WebQ.CookieContainer;
                return Key;
            }
        }

        /// <summary>
        /// 获取验证码图片
        /// </summary>
        /// <returns></returns>
        public static Bitmap getVerCodeImage() {
            Init();
            HttpWebRequest WebQ = (HttpWebRequest)WebRequest.Create("http://passport.bilibili.com/captcha?_=" + new Random().NextDouble().ToString());
            WebQ.CookieContainer = Cookie;
            using (var WebR = (HttpWebResponse)WebQ.GetResponse()) {
                var Stream = WebR.GetResponseStream();
                Image Img = Image.FromStream(Stream);
                Cookie = WebQ.CookieContainer;
                return new Bitmap(Img);
            }
        }

        /// <summary>
        /// 登录B站
        /// </summary>
        /// <param name="UserName">用户名</param>
        /// <param name="Password">密码</param>
        /// <param name="Code">验证码</param>
        /// <returns></returns>
        public static string LoginBilibili(string UserName, string Password, string Code) {
            string Hash;
            string Key = GetPublicKey(out Hash).Replace("\\n", "");
            Password = Common.RSAFromPkcs8.encryptData(Hash + Password, Key, "utf-8");

            string PostData = $"userid={System.Web.HttpUtility.UrlEncode(UserName, Encoding.UTF8)}&pwd={System.Web.HttpUtility.UrlEncode(Password, Encoding.UTF8)}&captcha={Code}&keep=1";
            HttpWebRequest WebQ = (HttpWebRequest)WebRequest.Create("https://passport.bilibili.com/ajax/miniLogin/login");
            WebQ.Method = "POST";
            WebQ.Referer = "http://passport.bilibili.com/ajax/miniLogin/minilogin";
            WebQ.ContentType = "application/x-www-form-urlencoded";
            WebQ.UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.4.1000 Chrome/39.0.2146.0 Safari/537.36";
            WebQ.CookieContainer = Cookie;
            byte[] bytesData = Encoding.UTF8.GetBytes(PostData);

            WebQ.ContentLength = bytesData.Length;
            using (Stream postStream = WebQ.GetRequestStream()) {
                postStream.Write(bytesData, 0, bytesData.Length);
            }
            HttpWebResponse res = ((HttpWebResponse)(WebQ.GetResponse()));
            using (StreamReader reader = new StreamReader(res.GetResponseStream(), Encoding.Default)) {
                string respHTML = reader.ReadToEnd();
                return respHTML;
            }
        }
    }
}
