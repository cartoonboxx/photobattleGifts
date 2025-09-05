import { User } from './user.entity';
export declare class Prize {
    id: number;
    prize_size: number;
    channel_link: string;
    winners_count: number;
    duration_minutes: number;
    created: Date;
    telegram_post_id: number;
    isFinished: boolean;
    channels: number[];
    users: User[];
}
