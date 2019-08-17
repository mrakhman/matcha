import axios_module from 'axios'

function init_axios(url, on_resp, on_err) {
    let axios = axios_module.create({
        baseURL: url,
        timeout: 20000,
        withCredentials: true
    });
    axios.interceptors.response.use((resp) => {
        if (on_resp === null){
            return resp;
        } else {
            return on_resp(resp)
        }
    }, (err) => {
        if (on_err === null) {
            return err;
        } else {
            return on_err(err)
        }
    });
    return axios
}
export default init_axios
