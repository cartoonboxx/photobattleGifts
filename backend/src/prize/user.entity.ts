import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Prize } from './prize.entity';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'bigint', unique: true })
  telegram_id: number;

  @Column({ type: 'varchar', nullable: true })
  username: string;

  @ManyToOne(() => Prize, (prize) => prize.users, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'prize_id' })
  prize: Prize;
}
