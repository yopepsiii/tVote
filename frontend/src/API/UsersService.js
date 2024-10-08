import $api from "./http/tVoteAPI";

export class UsersService {
    static async getMe() {
        const res = await $api.get('/users/me');
        return res.data;
    }

    // доделать полное взаимодействие с API
}