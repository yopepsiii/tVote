import $api from "./http/tVoteAPI"
import toast from "react-hot-toast";
import {VoteService} from "./VoteService";


export default class AuthService {

    static async Login(email, password) {
        const data = new FormData();
        data.append('username', email);
        data.append('password', password);

        try {
            const res = await $api.post('/login', data);
            localStorage.setItem('access_token', res.data.access_token)
            return res;
        }
        catch (e) {
            if (e.response.status === 401) {
                toast.error('Ошибка авторизации, перезагрузите страницу.')
            }
            else if (e.response.status === 403) {
                toast.error('Неверно введены почта или пароль.')
            }
            else if (e.response.status === 422) {
                toast.error('Нельзя оставлять форму пустой.')
            }
            else {
                toast.error(e.message)
            }

        }


    }

}