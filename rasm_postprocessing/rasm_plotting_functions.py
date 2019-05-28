#!/bin/env python 

def draw_map(lw=0.3):
    wr50a_map.m.drawmapboundary(fill_color=(0.9, 0.9, 0.9))
    wr50a_map.m.fillcontinents(color='white', zorder=0)
    wr50a_map.m.drawparallels(np.arange(-80., 81., 20.), linewidth=lw)
    wr50a_map.m.drawmeridians(np.arange(-180., 181., 20.), linewidth=lw)
    wr50a_map.m.drawcoastlines(color='k', linewidth=lw)

def plot_n_std_anoms(monthly_means, vmin=-25, vmax=25, smin=0, smax=3, amin=-4.5, amax=4.5,
                     cmap='Spectral_r', smap='YlGnBu', amap='RdBu', cbar_extend='both',
                     sbar_extend='max', abar_extend='both', cbar_label= 'Mean', varname=None, units='-'):
    with sns.axes_style("white"):

        # Set colorbar norms and ticks
        # assert(type(cmap) == str)
        cn = 10
        cmap = cmap_discretize(cmap, n_colors=cn)
        cnorm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        cticks = np.linspace(vmin, vmax, num=cn + 1)
        # assert(type(smap) == str)
        cn = 10
        smap = cmap_discretize(smap, n_colors=cn)
        snorm = mpl.colors.Normalize(vmin=smin, vmax=smax)
        sticks = np.linspace(smin, smax, num=cn + 1)
        # assert(type(amap) == str)
        an = 9
        amap = cmap_discretize(amap, n_colors=an)
        anorm = mpl.colors.Normalize(vmin=amin, vmax=amax)
        aticks = np.round(np.linspace(amin, amax, num=an + 1), 1)

        keys = list(monthly_means.keys())

        dss = monthly_means[keys[0]].resample('QS-SEP', dim='time').groupby('time.season')
        dsa = monthly_means[keys[0]].resample('AS', dim='time')

        nrows = len(monthly_means) + 1
        ncols = 5
        width = 11
        height = 1.55 * nrows + 0.6

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, 
                                 figsize=(width, height),
                                 sharex=True, sharey=True)
        plt.subplots_adjust(left=0.125, bottom=0.05,
                            right=0.9, top=0.9,
                            wspace=0.05, hspace=0.05)

        season_means = dss.mean(dim='time')
        season_stds = dss.std(dim='time')

        annual_means = dsa.mean(dim='time')
        annual_stds = dsa.std(dim='time')

        # Means
        for i, season in enumerate(seasons):
            plt.sca(axes[0, i])
            draw_map()
            sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, season_means.sel(season=season).to_masked_array()),
                            map_obj=wr50a_map, cbar=None, vmin=vmin, vmax=vmax, cmap=cmap)


        plt.sca(axes[0, 4])
        draw_map() 
        sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, annual_means.to_masked_array()),
                        map_obj=wr50a_map, cbar=None, vmin=vmin, vmax=vmax, cmap=cmap)    

        # Standard deviations
        for i, season in enumerate(seasons):
            plt.sca(axes[1, i])
            draw_map()
            sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, season_stds.sel(season=season).to_masked_array()),
                            map_obj=wr50a_map, cbar=None, vmin=smin, vmax=smax, cmap=smap)


        plt.sca(axes[1, 4])
        draw_map()
        sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, annual_stds.values.squeeze()),
                        map_obj=wr50a_map, cbar=None, vmin=smin, vmax=smax, cmap=smap)

        # anomalies
        for j, key in enumerate(keys[1:]):
            dss = monthly_means[key].resample('QS-SEP', dim='time').groupby('time.season')
            dsa = monthly_means[key].resample('AS', dim='time')
            season_anoms = (season_means - dss.mean(dim='time'))
            annual_anoms = (annual_means - dsa.mean(dim='time'))

            for i, season in enumerate(seasons):
                plt.sca(axes[j + 2, i])
                draw_map()
                sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, season_anoms.sel(season=season).to_masked_array()),
                                map_obj=wr50a_map, cbar=None, vmin=amin, vmax=amax, cmap=amap)


            plt.sca(axes[j + 2, 4])
            draw_map()
            sub_plot_pcolor(np.ma.masked_where(spatial_plot_mask, annual_anoms.to_masked_array()),
                            map_obj=wr50a_map, cbar=None, vmin=amin, vmax=amax, cmap=amap, ax=axes[j + 2, 4])

            # draw_map()

        plt.tight_layout()

        # titles = [ax.set_title(str(title)) for title, ax in zip(list(seasons) + ['Annual'], axes[0])]
        new_seasons = list(seasons) + ['Annual']
        for i, ax in enumerate(axes[0]):
            ax.set_title(new_seasons[i])
        # ylabels = [ax.set_ylabel("{0}\n — {1}".format(keys[0], label)) for label, ax in zip(keys[1:], axes[2:, 0])]
        for label, ax in zip(keys[1:], axes[2:, 0]): 
            # ax.set_ylabel("{0}\n — {1}".format(keys[0], label))
            ax.set_ylabel("%s \n - %s" % (keys[0], label))
        axes[0, 0].set_ylabel(keys[0])
        axes[1, 0].set_ylabel("{0} (Std.)".format(keys[0]))

        # Colorbars
        cbar_height = 0.02
        cbar_width = .313
        ax1 = fig.add_axes([0.01, -cbar_height, cbar_width, cbar_height])
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap, norm=cnorm,
                                        orientation='horizontal',
                                        extend=cbar_extend,
                                        ticks=cticks)
        ax2 = fig.add_axes([0.343, -cbar_height, cbar_width, cbar_height])
        cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=smap, norm=snorm,
                                        orientation='horizontal',
                                        extend=sbar_extend,
                                        ticks=sticks)
        ax3 = fig.add_axes([0.673, -cbar_height, cbar_width, cbar_height])
        cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=amap, norm=anorm,
                                        orientation='horizontal',
                                        extend=abar_extend,
                                        ticks=aticks)
        if varname is not None:
            cb1.set_label("{0} ({1}, Mean)".format(varname, units))
            cb2.set_label("{0} ({1}, Std.)".format(varname, units))
            cb3.set_label("{0} ({1}, Anomaly)".format(varname, units))

    return fig, axes
