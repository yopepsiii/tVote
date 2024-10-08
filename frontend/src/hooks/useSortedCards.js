import {useMemo} from "react";

export const useSortedCards = (cards) => {
    return useMemo(() => {
        return [...cards].sort((a, b) => (b['likes_count'] - b['dislikes_count']) - (a['likes_count'] - a['dislikes_count']));
    }, [cards])
}