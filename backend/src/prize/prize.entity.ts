import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  CreateDateColumn,
} from 'typeorm';
import { User } from './user.entity';

@Entity('prizes')
export class Prize {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int' })
  prize_size: number;

  @Column({ type: 'varchar' })
  channel_link: string;

  @Column({ type: 'int' })
  winners_count: number;

  @Column({ type: 'int' })
  duration_minutes: number;

  @CreateDateColumn()
  created: Date;

  @Column({ type: 'int' })
  telegram_post_id: number;

  @Column({ type: 'boolean', default: false })
  isFinished: boolean;

  @Column('bigint', { array: true, default: '{}' })
  channels: number[];

  @OneToMany(() => User, (user) => user.prize, { cascade: true })
  users: User[];
}
