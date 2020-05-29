from rest_framework import serializers


from .models import Category, Product, Variation, ProductFeatured, Company, GenericName, Brand, ProductUnit, ProductImage




class ImageSerializer(serializers.ModelSerializer):
	# discount = serializers.SerializerMethodField()
	class Meta:
		model = ProductImage
		fields = '__all__'




class VariationSerializer(serializers.ModelSerializer):
	discount = serializers.SerializerMethodField()
	class Meta:
		model = Variation
		fields = [
			"id",
			"title",
			"price",
			'sale_price',
			'discount'
		]

	def get_discount(self, obj):
		if obj.sale_price is None:
			return ""
		else:
			price = obj.price
			sale_price = obj.sale_price
			discount = round(((float(price)-float(sale_price))/float(price))*100, 2)			
			return discount


		# return float(price - sale_price)
		# if self.sale_price:
		# 	return self.price
		# return ""
		# print(self.price)	


class ProductDetailUpdateSerializer(serializers.ModelSerializer):
	variation_set = VariationSerializer(many=True, read_only=True)
	
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"id",
			"title",
			"description",
			"price",
			"image",
			"variation_set",
			
		]


	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None



	def create(self, validated_data):
		title = validated_data["title"]
		Product.objects.get(title=title)
		product = Product.objects.create(**validated_data)
		return product

	def update(self, instance, validated_data):
		instance.title = validated_data["title"]
		instance.save()
		return instance
	# def update


class ProductDetailSerializer(serializers.ModelSerializer):
	variation_set = VariationSerializer(many=True, read_only=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"id",
			"title",
			"description",
			"price",
			"image",
			"variation_set",
		]

	def get_image(self, obj):
		image_url = obj.productimage_set.first().image.url
		return image_url
		#return obj.productimage_set.first().image.url
		 





class ProductSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	productimage_set = ImageSerializer(many=True, read_only=True)
	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"variation_set",
			"productimage_set"
		]

	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None

	# def get_images_set(self, obj):
	# 	try:
	# 		# return obj.productimage_set.filter().image.url
	# 		return ProductImage.objects.filter(product_id=2).get().__dict__['image']
	# 	except:
	# 		return None


class ProductFilterSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"variation_set",
		]

	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None


class ProductFeaturedSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"variation_set",
		]

	
	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None


class SubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'title']



class CategorySerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='category_detail_api')
	product_set = ProductSerializer(many=True)
	# fk_category = SubCategorySerializer(many=True)
	children_list = serializers.SerializerMethodField('_get_children')
	def _get_children(self, obj):
		serializer = SubCategorySerializer(Category.objects.filter(fk_category=obj.id), many=True)
		return serializer.data


	class Meta:
		model = Category
		fields = [
			"url",
			"id",
			"title",
			"image",
			"description",
			"product_set", ## obj.product_set.all()
			"children_list"
			# 'fk_category'
			#"default_category",

		]


class CompanySerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = Company
		fields = ['id','title'] 


class GenericNameSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = GenericName
		fields = ['id','title'] 


class BrandSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = Brand
		fields = ['id','title'] 


class ProductUnitSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = ProductUnit
		fields = ['id','title'] 

#CREATE RETRIEVE UPDATE DESTROY