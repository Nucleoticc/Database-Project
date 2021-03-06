export default {
    setStudent(state, payload) {
        state.students = payload;
    },
    setFetchTimestamp(state){
        state.lastFetch = new Date().getTime();
    }
}