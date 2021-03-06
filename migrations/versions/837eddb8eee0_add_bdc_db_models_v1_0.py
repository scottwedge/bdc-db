"""add bdc-db models v1.0

Revision ID: 837eddb8eee0
Revises: 
Create Date: 2019-12-06 22:59:26.666832

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '837eddb8eee0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('composite_function_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grs_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('raster_size_schemas',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('raster_size_x', sa.Float(precision=53), nullable=False),
    sa.Column('raster_size_y', sa.Float(precision=53), nullable=False),
    sa.Column('raster_size_t', sa.Float(precision=53), nullable=True),
    sa.Column('chunk_size_x', sa.Float(precision=53), nullable=False),
    sa.Column('chunk_size_y', sa.Float(precision=53), nullable=False),
    sa.Column('chunk_size_t', sa.Float(precision=53), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('temporal_composition_schemas',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('temporal_composite_unit', sa.String(length=16), nullable=False),
    sa.Column('temporal_schema', sa.String(length=16), nullable=False),
    sa.Column('temporal_composite_t', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collections',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('temporal_composition_schema_id', sa.String(length=20), nullable=True),
    sa.Column('raster_size_schema_id', sa.String(length=60), nullable=True),
    sa.Column('composite_function_schema_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('sensor', sa.String(length=40), nullable=True),
    sa.Column('geometry_processing', sa.String(length=16), nullable=True),
    sa.Column('radiometric_processing', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('oauth_scope', sa.String(length=250), nullable=True),
    sa.Column('is_cube', sa.Boolean(), nullable=True),
    sa.Column('bands_quicklook', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['composite_function_schema_id'], ['composite_function_schemas.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['raster_size_schema_id'], ['raster_size_schemas.id'], ),
    sa.ForeignKeyConstraint(['temporal_composition_schema_id'], ['temporal_composition_schemas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tiles',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('geom_wgs84', geoalchemy2.types.Geometry(spatial_index=False), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(spatial_index=False), nullable=True),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.PrimaryKeyConstraint('id', 'grs_schema_id'),
    sa.UniqueConstraint('id')
    )
    op.create_index('idx_tiles_geom', 'tiles', ['geom'], unique=False, postgres_using='gist')
    op.create_index('idx_tiles_geom_wgs84', 'tiles', ['geom_wgs84'], unique=False, postgres_using='gist')
    op.create_table('bands',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('min', sa.Float(), nullable=True),
    sa.Column('max', sa.Float(), nullable=True),
    sa.Column('fill', sa.Integer(), nullable=True),
    sa.Column('scale', sa.String(length=16), nullable=True),
    sa.Column('common_name', sa.String(length=16), nullable=False),
    sa.Column('data_type', sa.String(length=16), nullable=True),
    sa.Column('mime_type', sa.String(length=16), nullable=True),
    sa.Column('resolution_x', sa.Float(precision=53), nullable=False),
    sa.Column('resolution_y', sa.Float(precision=53), nullable=False),
    sa.Column('resolution_unit', sa.String(length=16), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.PrimaryKeyConstraint('id', 'name', 'collection_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('collection_items',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.Column('item_date', sa.Date(), nullable=False),
    sa.Column('composite_start', sa.Date(), nullable=False),
    sa.Column('composite_end', sa.Date(), nullable=True),
    sa.Column('quicklook', sa.Text(), nullable=True),
    sa.Column('cloud_cover', sa.Float(), nullable=True),
    sa.Column('scene_type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id', 'grs_schema_id', 'tile_id', 'item_date'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_collection_items_composite_end'), 'collection_items', ['composite_end'], unique=False)
    op.create_index(op.f('ix_collection_items_composite_start'), 'collection_items', ['composite_start'], unique=False)
    op.create_table('collection_tiles',
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('collection_id', 'grs_schema_id', 'tile_id')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.String(length=20), nullable=False),
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.Column('grs_schema_id', sa.String(length=20), nullable=False),
    sa.Column('tile_id', sa.String(length=20), nullable=False),
    sa.Column('collection_item_id', sa.String(length=64), nullable=False),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('source', sa.String(length=30), nullable=True),
    sa.Column('raster_size_x', sa.Float(precision=53), nullable=True),
    sa.Column('raster_size_y', sa.Float(precision=53), nullable=True),
    sa.Column('raster_size_t', sa.Float(precision=53), nullable=True),
    sa.Column('chunk_size_x', sa.Float(precision=53), nullable=True),
    sa.Column('chunk_size_y', sa.Float(precision=53), nullable=True),
    sa.Column('chunk_size_t', sa.Float(precision=53), nullable=True),
    sa.ForeignKeyConstraint(['band_id'], ['bands.id'], ),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['collection_item_id'], ['collection_items.id'], ),
    sa.ForeignKeyConstraint(['grs_schema_id'], ['grs_schemas.id'], ),
    sa.ForeignKeyConstraint(['tile_id'], ['tiles.id'], ),
    sa.PrimaryKeyConstraint('id', 'collection_id', 'band_id', 'grs_schema_id', 'tile_id', 'collection_item_id')
    )
    op.create_index(op.f('ix_assets_collection_item_id'), 'assets', ['collection_item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assets_collection_item_id'), table_name='assets')
    op.drop_table('assets')
    op.drop_table('collection_tiles')
    op.drop_index(op.f('ix_collection_items_composite_start'), table_name='collection_items')
    op.drop_index(op.f('ix_collection_items_composite_end'), table_name='collection_items')
    op.drop_table('collection_items')
    op.drop_table('bands')
    op.drop_index('idx_tiles_geom_wgs84', table_name='tiles')
    op.drop_index('idx_tiles_geom', table_name='tiles')
    op.drop_table('tiles')
    op.drop_table('collections')
    op.drop_table('temporal_composition_schemas')
    op.drop_table('raster_size_schemas')
    op.drop_table('grs_schemas')
    op.drop_table('composite_function_schemas')
    # ### end Alembic commands ###
