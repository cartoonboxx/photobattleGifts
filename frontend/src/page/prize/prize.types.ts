export interface PrizeObj {
  id?: number;
  prize_count: number;
  channel_link: string;
  created: string;
  channels: number[];
  duration_minutes: number;
  isFinished: boolean;
}

export interface UserObj {
  id?: number;
  telegram_id: number;
  username: string;
  prize?: PrizeObj;
}
