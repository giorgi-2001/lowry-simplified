import { useState, FocusEvent } from "react"


const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/


const useValidateForm = () => {
    const [usernameError, setUsernameError] = useState("")
    const [emailError, setEmailError] = useState("")
    const [passwordError, setPasswordError] = useState("")
    const [password2Error, setPassword2Error] = useState("")


    const validateUsername = (e: FocusEvent<HTMLInputElement>) => {
        if (e.target.value.length < 4) {
            setUsernameError("Username must be at least 4 characters long!")
        } else {
            setUsernameError("")
        }
    }

    const validateEmail = (e: FocusEvent<HTMLInputElement>) => {
        if (!e.target.value || !emailRegex.test(e.target.value)) {
            setEmailError("Must be valid email!")
        } else {
            setEmailError("")
        }
    }

    const validatePassword = (e: FocusEvent<HTMLInputElement>) => {
        if (e.target.value.length < 8) {
            setPasswordError("Password must be at leat 8 characters long!")
        } else {
            setPasswordError("")
        }
    }

    const validatePassword2 = (e: FocusEvent<HTMLInputElement>, password: string) => {
        if (e.target.value !== password) {
            setPassword2Error("Passwords do not match!")
        } else {
            setPassword2Error("")
        }
    }

    return {
        usernameError, validateUsername,
        emailError, validateEmail,
        passwordError, validatePassword,
        password2Error, validatePassword2
    }
}


export default useValidateForm