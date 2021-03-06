export default {
    setExaminer(state, payload) {
        state.examiners = payload;
    },
    setFetchTimestamp(state){
        state.lastFetch = new Date().getTime();
    }
}