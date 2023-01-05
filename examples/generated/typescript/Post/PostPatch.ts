import { UserPatch } from '../User/UserPatch';

export interface PostPatch {
    title?: string,
    content?: string,
    published_at?: Date,
    status?: 'DELETED'|'PUBLISHED',
    user?: UserPatch,
    id: number,
}