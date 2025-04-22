import { auth } from "./firebase";
import { signOut } from "firebase/auth";

export default async function handleLogout(navigate){

    try{
        await signOut(auth);
        navigate("/");
    }catch (error){
        alert("Error logging out: ",error);
    }
}