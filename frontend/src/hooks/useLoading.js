import {useState} from "react";

export const useLoading = (callback) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetching = async () => {
        try {
            setIsLoading(true);
            setError(null)
            await callback()
        }
        catch (e) {
            if (e.response) {
                setError(e.response.data.detail)
            }
            else {
                setError(e.message)
            }

        }

        finally {
            setIsLoading(false)
        }

    }

    return [fetching, isLoading, error]
}