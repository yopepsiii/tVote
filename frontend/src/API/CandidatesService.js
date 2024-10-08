import $api from "./http/tVoteAPI";

export class CandidatesService {
    static async getCandidates() {
        const res = await $api.get('/candidates/');
        return res.data;
    }

    static async getProfburoMembers() {
        const res = await $api.get('/candidates/profburo');
        return res.data;
    }

    // добавить полное взаимодействие с API
}