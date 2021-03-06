export default {
    setCategories(state, payload) {
        state.categories = payload;
    },
    setStatus(state, payload){
        const id = payload.id;
        const active_category = state.categories.filter((category)=>category.id != id);
        const changed_category = state.categories.filter((category)=>category.id == id);
        changed_category[0].status = 'Active';
        active_category.push(changed_category[0]);
        console.log(active_category);
        state.categories = active_category;
    },
    setFetchTimestamp(state){
        state.lastFetch = new Date().getTime();
    }
}