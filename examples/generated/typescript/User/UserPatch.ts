import { PostPatch } from '../Post/PostPatch';

export interface UserPatch {
    email?: string,
    firstname?: string,
    lastname?: string,
    posts?: PostPatch,
    id: number,
}