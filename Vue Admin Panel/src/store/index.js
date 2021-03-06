import { createStore } from 'vuex';

import authModule from './login/index.js';
import studentModule from './students/index.js';
import examinerModule from './examiners/index.js';
import categoryModule from './categories/index.js';

const store = createStore({
    modules:{
        auth: authModule,
        students: studentModule,
        examiners: examinerModule,
        categories: categoryModule
    }
});

export default store;