import $api from "./http/tVoteAPI";

export class VoteService {
    static async voteToCandidate(candidate_id, type) {
        const data = {
            candidate_id,
            type
        }
        return await $api.post('/votes/', data)


    }

    static async voteToProfburo(type) {
        const data = {
            'type' : type
        }
        return await $api.post('/votes/profburo', data)
    }
}