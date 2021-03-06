import axios from 'axios';

export default {
  async loadExaminers(context, payload) {
    if (!payload.forceRefresh && !context.getters.shouldUpdate) {
      return;
    }
    await axios.get(
      'http://127.0.0.1:5000/api/admin/examiner'
    ).then((response)=>{
      const responseData = response.data['examiners'];
      const examiners = [];
      for (const key in responseData){
        const examiner = {
          id: responseData[key].id,
          fname: responseData[key].fname,
          lname: responseData[key].lname,
          email: responseData[key].email,
          uname: responseData[key].uname
        }
        examiners.push(examiner);
      }
      context.commit('setExaminer', examiners);
      context.commit('setFetchTimestamp');
    }).catch((err)=>{
      console.log(err);
    });
  }
};
