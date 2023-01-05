import { PostCreate } from '../Post/PostCreate';

export interface UserCreate {
    email: string,
    firstname: string,
    lastname: string,
    posts: PostCreate,
}