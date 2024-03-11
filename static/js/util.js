export function checkPassword(password) {
    let hasLower = false;
    let hasUpper = false;
    let hasDigit = false;
    let hasSpecial = false;
    const specialCharacters = "@$!%*?&";

    // check password length
    if (password.length < 8) {
        return false;
    }

    // must contain lowercase, uppercase, digit and special character
    for (let i = 0; i < password.length; i++) {
        const char = password[i];
        if (char >= 'a' && char <= 'z') {
            hasLower = true;
        } else if (char >= 'A' && char <= 'Z') {
            hasUpper = true;
        } else if (char >= '0' && char <= '9') {
            hasDigit = true;
        } else if (specialCharacters.includes(char)) {
            hasSpecial = true;
        }
    }

    return hasLower && hasUpper && hasDigit && hasSpecial;
}