import axios from 'axios';

export default {
  async login(context, payload) {
    let url = "http://127.0.0.1:5000/api/admin/login";
    await axios.post(url, {
      email: payload.email,
      password: payload.password
    }).then((data)=>{
      sessionStorage.setItem("token", data.data.token);
      sessionStorage.setItem("userId", data.data.userId);
      context.commit("setUser", {
        token: data.data.token,
        userId: data.data.userId
      })
    }).catch((err)=>{
      console.log(err)
    });
  },
  tryLogin(context) {
    const token = sessionStorage.getItem('token');
    const userId = sessionStorage.getItem('userId');

    if (token && userId) {
      context.commit('setUser', {
        token: token,
        userId: userId
      });
    }
  },
  logout(context) {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("userId");
    
    context.commit("setUser", {
      token: null,
      userId: null,
    });
  },
};
