import { Repository } from 'typeorm';
import { Prize } from './prize.entity';
import { User } from './user.entity';
export declare class PrizesService {
    private prizeRepo;
    private userRepo;
    constructor(prizeRepo: Repository<Prize>, userRepo: Repository<User>);
    getPrizeById(id: number): Promise<Prize>;
    getUsersByPrize(id: number): Promise<User[]>;
    addUserToPrize(prizeId: number, telegram_id: number, username?: string): Promise<User>;
    removeUserFromPrize(prizeId: number, telegram_id: number): Promise<void>;
    updatePrize(id: number, data: Partial<Prize>): Promise<Prize>;
}
