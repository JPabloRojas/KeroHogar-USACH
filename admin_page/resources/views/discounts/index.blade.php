@extends('layouts.app')

@section('style')
@endsection

@section('content')
<div class="container-fluid">
    <div class="row">
        <div class="col-md-12">
            <div class="float-right mr-3 mb-2">
                <a class="btn btn-success" href="{{ route('discounts.create', $product->id) }}"> {{__('navigation.discounts.create')}} </a>
            </div>
        </div>
    </div>
    @include('partials.session_success')
    <div class="row px-3">
        <div class="col-md-12">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <td>N°</td>
                        <td colspan="3">Acciones</td>
                    </tr>
                </thead>
                <tbody>
                    @foreach($priceDiscounts as $priceDiscount)
                    <tr>
                        <td>{{ ++$rowItem }}</td>
                        <td><a href="{{ route('discounts.show', [$product->id, $priceDiscount->id]) }}" class="btn btn-info">{{__('navigation.show')}}</a></td>
                        <td><a href="{{ route('discounts.edit', [$product->id, $priceDiscount->id]) }}" class="btn btn-primary">{{__('navigation.edit')}}</a></td>
                        <td>
                            <form action="{{ route('discounts.destroy', [$product->id, $priceDiscount->id]) }}" method="post">
                                @csrf
                                @method('DELETE')
                                <button class="btn btn-danger delete" data-confirm="{{__('navigation.confirm_deletion')}}" type="submit">{{__('navigation.delete')}}</button>
                            </form>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>

            {!! $priceDiscounts->links() !!}
        </div>
    </div>
</div>
@endsection

@section('script')
<script src="{{ asset('js/confirm_deletion.js') }}" defer></script>
@endsection