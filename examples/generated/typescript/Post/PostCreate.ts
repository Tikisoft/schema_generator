import { UserCreate } from '../User/UserCreate';

export interface PostCreate {
    title: string,
    content: string,
    published_at: Date,
    status: 'DELETED'|'PUBLISHED',
    user: UserCreate,
}