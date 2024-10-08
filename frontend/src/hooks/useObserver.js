import {useEffect, useRef} from "react";

export const useObserver = (ref, canLoad, isLoading, callback) => {
    let observer = useRef()
    const observeOptions = {
        rootMargin: "5px",
        threshold: 0
    }

    useEffect(() => {
        if (isLoading) return;
        if (observer.current) observer.current.disconnect();
        let cb = (entries) => {

            if (entries[0].isIntersecting && canLoad) {
                callback()
            }
        }

        observer.current = new IntersectionObserver(cb, observeOptions);
        observer.current.observe(ref.current)
    }, [isLoading, ref]);
}