<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Carbon;

class TimeBlock extends Model
{
    const ITEMS_PER_PAGE = 10;
    
    public $guarded = [];

    protected $dates = [
        'created_at',
        'updated_at',
    ];

    public function orders() {
        return $this->belongsToMany('App\Order')->withTimestamps();
    }

    public function scopeOrderedBlocksPaginated($query) {
        return $query->orderBy('start', 'asc')->paginate(self::ITEMS_PER_PAGE);
    }

    public function getStartAttribute($time) {
        return Carbon::parse($time)->format('H:i');
    }

    public function getEndAttribute($time) {
        return Carbon::parse($time)->format('H:i');
    }
}
