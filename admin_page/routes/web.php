<?php
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return redirect()->to(route('login'));
});

Auth::routes();

Route::middleware('auth')->group( function() {
    Route::resource('pedidos', 'OrderController')->names([
        'index' => 'orders.index',
        'create' => 'orders.create',
        'store' => 'orders.store',
        'show' => 'orders.show',
        'edit' => 'orders.edit',
        'update' => 'orders.update',
        'destroy' => 'orders.destroy',
    ])->parameters([
        'pedidos' => 'order'
    ]);

    Route::resource('productos', 'ProductController')->names([
        'index' => 'products.index',
        'create' => 'products.create',
        'store' => 'products.store',
        'show' => 'products.show',
        'edit' => 'products.edit',
        'update' => 'products.update',
        'destroy' => 'products.destroy',
    ])->parameters([
        'productos' => 'product',
    ]);
    
    Route::resource('productos/{product}/descuentos', 'PriceDiscountController')->names([
        'index' => 'discounts.index',
        'create' => 'discounts.create',
        'store' => 'discounts.store',
        'show' => 'discounts.show',
        'edit' => 'discounts.edit',
        'update' => 'discounts.update',
        'destroy' => 'discounts.destroy',
    ])->parameters([
        'descuentos' => 'priceDiscount',
    ]);

    Route::resource('horario', 'TimeBlockController')->names([
        'index' => 'schedule.index',
        'create' => 'schedule.create',
        'store' => 'schedule.store',
        'show' => 'schedule.show',
        'edit' => 'schedule.edit',
        'update' => 'schedule.update',
        'destroy' => 'schedule.destroy',
    ])->parameters([
        'horario' => 'timeBlock',
    ]);
    
});