import axios from 'axios';

export default {
  async loadCategories(context, payload) {
    if (!payload.forceRefresh && !context.getters.shouldUpdate) {
      return;
    }
    await axios.get(
      'http://127.0.0.1:5000/api/admin/categories'
    ).then((response)=>{
      const responseData = response.data['categories'];
      const categories = [];
      for (const key in responseData){
        const category = {
          id: responseData[key].id,
          name: responseData[key].name,
          description: responseData[key].description,
          status: responseData[key].status
        }
        categories.push(category);
      }
      context.commit('setCategories', categories);
      context.commit('setFetchTimestamp');
    }).catch((err)=>{
      console.log(err);
    });
  },
  async activateCategory(context, payload){
    await axios.put(
      'http://127.0.0.1:5000/api/admin/categories', {
        'category_id': payload.id
      }). then((data)=>{
        console.log(data);
      }).catch((err)=>{
        console.log(err);
      });
    context.commit('setStatus', payload);
  }
};
