import axios from 'axios';

export default {
  async loadStudents(context, payload) {
    if (!payload.forceRefresh && !context.getters.shouldUpdate) {
      return;
    }
    await axios.get(
      'http://127.0.0.1:5000/api/admin/student'
    ).then((response)=>{
      const responseData = response.data['students'];
      const students = [];
      for (const key in responseData){
        const student = {
          id: responseData[key].id,
          fname: responseData[key].fname,
          lname: responseData[key].lname,
          email: responseData[key].email,
          uname: responseData[key].uname,
          attempted: responseData[key].attempted,
          solved: responseData[key].solved,
          score: responseData[key].score,
        }
        students.push(student);
      }
      context.commit('setStudent', students);
      context.commit('setFetchTimestamp');
    }).catch((err)=>{
      console.log(err);
    });
  }
};
